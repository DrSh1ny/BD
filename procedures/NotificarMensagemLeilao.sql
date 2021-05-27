CREATE OR REPLACE FUNCTION notifyOnBoardPost()
	RETURNS TRIGGER
LANGUAGE 'plpgsql'
AS $BODY$
declare
    f record;
	f2 record;
	msg text;
	dt TIMESTAMP;
	c1 cursor(idPessoa bigint) for
        select *
        from pessoa
        where pessoa.id=idPessoa;
begin
    open c1(new.pessoa_id);
	fetch c1 into f2;
	close c1;
	msg:='O licitador ' || f2.nome || ' escreveu no moral do leilao ' || new.leilao_id || ': ' || new.titulo;
	dt:= CURRENT_TIMESTAMP;
	insert into notificacao(mensagem,data) values (msg,dt);
	for f in 
		select * from PeopleInAuctionBoard(new.leilao_id)
		union
		select * from PeopleInAuctionLicitations(new.leilao_id)
    loop 
		insert into notificacao_pessoa(lida,notificacao_data,pessoa_id) values(FALSE,dt,f.id);
    end loop;
	RETURN NEW;
end;
$BODY$;

DROP TRIGGER IF EXISTS notifyOnBoardPost
  ON mensagem;
CREATE TRIGGER notifyOnBoardPost 
   after insert
   ON mensagem
   FOR EACH ROW
       EXECUTE PROCEDURE notifyOnBoardPost();
