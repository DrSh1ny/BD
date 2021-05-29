CREATE OR REPLACE FUNCTION notifyOnLicitation()
	RETURNS TRIGGER
LANGUAGE 'plpgsql'
AS $BODY$
declare
	f record;
	f1 record;
	f2 record;
	msg text;
	dt TIMESTAMP;
	idNotificacao bigint;
	c1 cursor(idLeilao bigint) for
        select *
		from licitacao
		where licitacao.leilao_id=idLeilao and licitacao.preco=(select max(preco) from licitacao where licitacao.leilao_id=idLeilao);
	c3 cursor(idLeilao bigint) for
		select *
		from leilao
		where leilao.id=idLeilao;
begin
	msg:='Nova licitacao no leilao ' || new.leilao_id || ': ' || new.preco || '€';
	dt:= CURRENT_TIMESTAMP;
	insert into notificacao(mensagem,data) values (msg,dt) returning id into idNotificacao;
	
	open c3(new.leilao_id);
	fetch c3 into f2;
	close c3;
	insert into notificacao_pessoa(lida,pessoa_id,notificacao_id) values(FALSE,f2.pessoa_id,idNotificacao);
	
    open c1(new.leilao_id);
	fetch c1 into f;
	close c1;
	if(not found) then
		return new;
	end if;
	insert into notificacao_pessoa(lida,pessoa_id,notificacao_id) values(FALSE,f.pessoa_id,idNotificacao);
	return new;
end;
$BODY$;

DROP TRIGGER IF EXISTS notifyOnLicitation
  ON licitacao;
CREATE TRIGGER notifyOnLicitation 
   before insert
   ON licitacao
   FOR EACH ROW
       EXECUTE PROCEDURE notifyOnLicitation();